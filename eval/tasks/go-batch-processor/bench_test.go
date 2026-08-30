package solution

import (
	"errors"
	"testing"
)

func sum(batch []int) (int, error) {
	s := 0
	for _, v := range batch {
		s += v
	}
	return s, nil
}

func TestProcessBatchesOrder(t *testing.T) {
	got, err := ProcessBatches([]int{1, 2, 3, 4, 5}, 2, sum)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := []int{3, 7, 5}
	if len(got) != len(want) {
		t.Fatalf("len = %d, want %d (%v)", len(got), len(want), got)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("got %v, want %v", got, want)
		}
	}
}

func TestProcessBatchesAggregatesErrors(t *testing.T) {
	boom := errors.New("boom")
	fn := func(b []int) (int, error) {
		if b[0] == 3 {
			return 0, boom
		}
		return b[0], nil
	}
	if _, err := ProcessBatches([]int{1, 2, 3, 4}, 2, fn); err == nil {
		t.Fatal("expected an error")
	} else if !errors.Is(err, boom) {
		t.Fatalf("error does not match the batch error: %v", err)
	}
}

func TestProcessBatchesEdgeCases(t *testing.T) {
	if got, err := ProcessBatches(nil, 2, sum); err != nil || len(got) != 0 {
		t.Fatalf("nil items: got %v, %v", got, err)
	}
	if got, err := ProcessBatches([]int{1, 2}, 0, sum); err != nil || len(got) != 0 {
		t.Fatalf("batchSize 0: got %v, %v", got, err)
	}
}

// Harness-owned benchmark. It uses b.Loop() deliberately: that idiom is itself
// one of the guidelines under test, so the model must not supply it.
func BenchmarkProcessBatches(b *testing.B) {
	items := make([]int, 10_000)
	for i := range items {
		items[i] = i
	}
	b.ReportAllocs()
	for b.Loop() {
		if _, err := ProcessBatches(items, 100, sum); err != nil {
			b.Fatal(err)
		}
	}
}
