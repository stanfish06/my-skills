#!/usr/bin/env python3
"""
Remove or replace Protected Health Information (PHI) in a DICOM file.

WARNING — this is NOT a DICOM PS3.15 Annex E conformant de-identification
profile. It is a keyword allowlist and it cannot see PHI it does not enumerate:
identifiers nested inside Sequence Items, structured report content, overlays,
curves, retired attributes, or text burned into Pixel Data. Do not use it on
data leaving an institution. For conformant de-identification use
`pydicom/deid` (https://github.com/pydicom/deid) or `dicognito`
(https://github.com/blairconrad/dicognito), both MIT-licensed and maintained.

Usage:
    python anonymize_dicom.py input.dcm output.dcm
    python anonymize_dicom.py input.dcm output.dcm --patient-id ANON001
"""

import argparse
import sys
from pathlib import Path

try:
    import pydicom
except ImportError:
    print("Error: pydicom is not installed. Install it with: pip install pydicom")
    sys.exit(1)


# LO is limited to 64 bytes per value, so this is sent as multiple values.
DEID_METHOD = [
    "pydicom skill anonymize_dicom.py: top-level keyword allowlist",
    "private attributes removed, UIDs remapped",
    "NOT PS3.15 Annex E conformant",
]

# PS3.15 Annex E Table E.1-1, Basic Profile action X — remove the attribute,
# and all Items if it is a Sequence.
REMOVE_TAGS = [
    'PatientBirthTime',
    'PatientSex', 'PatientAge', 'PatientSize', 'PatientWeight',
    'PatientAddress', 'PatientTelephoneNumbers', 'PatientMotherBirthName',
    'OtherPatientIDs', 'OtherPatientNames',
    'MilitaryRank', 'EthnicGroup', 'Occupation', 'PatientComments',
    'InstitutionName', 'InstitutionAddress', 'InstitutionalDepartmentName',
    'ReferringPhysicianAddress',
    'ReferringPhysicianTelephoneNumbers', 'ReferringPhysicianIdentificationSequence',
    'PerformingPhysicianName', 'PerformingPhysicianIdentificationSequence',
    'OperatorsName', 'PhysiciansOfRecord', 'PhysiciansOfRecordIdentificationSequence',
    'NameOfPhysiciansReadingStudy', 'PhysiciansReadingStudyIdentificationSequence',
    'StudyDescription', 'SeriesDescription', 'AdmittingDiagnosesDescription',
    'DerivationDescription', 'RequestingPhysician', 'RequestingService',
    'RequestedProcedureDescription', 'ScheduledPerformingPhysicianName',
    'PerformedLocation', 'PerformedStationName',
    'RequestAttributesSequence',
    'SeriesDate', 'SeriesTime', 'AcquisitionDate', 'AcquisitionTime',
]

# Basic Profile action Z — replace with a zero-length value. These are Type 2 in
# their modules, so removing them would invalidate the IOD.
ZERO_LENGTH_TAGS = [
    'AccessionNumber', 'ReferringPhysicianName',
    'StudyDate', 'StudyTime', 'ContentDate', 'ContentTime',
]

# Basic Profile action U — replace with a UID that is "internally consistent
# within a set of Instances". Derived from the original UID so every file in a
# study or series maps to the same replacement across separate invocations.
UID_TAGS = [
    'StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID',
    'FrameOfReferenceUID',
]


def anonymize_dicom(input_path, output_path, patient_id='ANONYMOUS', patient_name='ANONYMOUS'):
    """
    Anonymize a DICOM file by removing or replacing PHI.

    Args:
        input_path: Path to input DICOM file
        output_path: Path to output anonymized DICOM file
        patient_id: Replacement patient ID (default: 'ANONYMOUS')
        patient_name: Replacement patient name (default: 'ANONYMOUS')

    Returns:
        (success, changes_or_error, warnings)
    """
    try:
        ds = pydicom.dcmread(input_path)

        anonymized = []
        warnings = []

        # Action Z with a dummy value
        ds.PatientName = patient_name
        anonymized.append(f"PatientName: replaced with '{patient_name}'")
        ds.PatientID = patient_id
        anonymized.append(f"PatientID: replaced with '{patient_id}'")
        ds.PatientBirthDate = '19000101'
        anonymized.append("PatientBirthDate: replaced with '19000101'")

        for tag in ZERO_LENGTH_TAGS:
            if hasattr(ds, tag):
                setattr(ds, tag, '')
                anonymized.append(f"{tag}: zero-length (action Z)")

        for tag in REMOVE_TAGS:
            if hasattr(ds, tag):
                delattr(ds, tag)
                anonymized.append(f"{tag}: removed (action X)")

        # Private Attributes are action X: many scanners store name, ID and
        # accession number here, so the allowlist alone leaves them intact.
        ds.remove_private_tags()
        anonymized.append("private attributes: removed (action X)")

        # Retained UIDs are a high-fidelity join key back to the source PACS.
        for tag in UID_TAGS:
            original = getattr(ds, tag, None)
            if original:
                setattr(ds, tag, pydicom.uid.generate_uid(entropy_srcs=[str(original)]))
                anonymized.append(f"{tag}: remapped (action U)")

        file_meta = getattr(ds, 'file_meta', None)
        if file_meta is not None and getattr(file_meta, 'MediaStorageSOPInstanceUID', None):
            file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
            anonymized.append("file_meta.MediaStorageSOPInstanceUID: synced to new SOPInstanceUID")

        # PS3.15 E.1.1 requires both of these on a de-identified Data Set.
        ds.PatientIdentityRemoved = 'YES'
        ds.DeidentificationMethod = DEID_METHOD
        anonymized.append("PatientIdentityRemoved / DeidentificationMethod: written")

        if str(ds.get('BurnedInAnnotation', '')).upper() != 'NO':
            warnings.append(
                "BurnedInAnnotation is not 'NO': Pixel Data may carry identifying "
                "text. Pixel Data is not modified by this script."
            )

        if any(elem.VR == 'SQ' for elem in ds):
            warnings.append(
                "Dataset contains Sequences. Identifiers inside Sequence Items are "
                "not reached by this keyword allowlist."
            )

        ds.save_as(output_path)

        return True, anonymized, warnings

    except Exception as e:
        return False, str(e), []


def main():
    parser = argparse.ArgumentParser(
        description='Remove or replace PHI in a DICOM file (not PS3.15 Annex E conformant)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python anonymize_dicom.py input.dcm output.dcm
  python anonymize_dicom.py input.dcm output.dcm --patient-id ANON001
  python anonymize_dicom.py input.dcm output.dcm --patient-id ANON001 --patient-name "Anonymous^Patient"
        """
    )

    parser.add_argument('input', type=str, help='Input DICOM file')
    parser.add_argument('output', type=str, help='Output anonymized DICOM file')
    parser.add_argument('--patient-id', type=str, default='ANONYMOUS',
                       help='Replacement patient ID (default: ANONYMOUS)')
    parser.add_argument('--patient-name', type=str, default='ANONYMOUS',
                       help='Replacement patient name (default: ANONYMOUS)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed anonymization information')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)

    print(f"Anonymizing: {args.input}")
    success, result, warnings = anonymize_dicom(args.input, args.output,
                                                args.patient_id, args.patient_name)

    if not success:
        print(f"✗ Error: {result}")
        sys.exit(1)

    print(f"Wrote {args.output} after applying {len(result)} changes.")
    if args.verbose:
        for item in result:
            print(f"  - {item}")

    for warning in warnings:
        print(f"! {warning}", file=sys.stderr)
    print(
        "! Not a PS3.15 Annex E conformant profile. Verify the output before it "
        "leaves the institution, or use pydicom/deid or dicognito instead.",
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
