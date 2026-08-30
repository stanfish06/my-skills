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
	// Two distinct failures, so an implementation that reports only the first
	// (or only the last) and wraps it in errors.Join cannot pass.
	errLow := errors.New("low batch failed")
	errHigh := errors.New("high batch failed")
	fn := func(b []int) (int, error) {
		switch b[0] {
		case 3:
			return 0, errLow
		case 7:
			return 0, errHigh
		}
		return b[0] * 100, nil
	}

	got, err := ProcessBatches([]int{1, 2, 3, 4, 5, 6, 7, 8}, 2, fn)
	if err == nil {
		t.Fatal("expected an error")
	}
	if !errors.Is(err, errLow) {
		t.Fatalf("first batch error is not discoverable in %v", err)
	}
	if !errors.Is(err, errHigh) {
		t.Fatalf("second batch error is not discoverable in %v", err)
	}

	// Results survive the failures, one entry per batch, still in batch order.
	want := []int{100, 0, 500, 0}
	if len(got) != len(want) {
		t.Fatalf("len = %d, want %d (%v)", len(got), len(want), got)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("got %v, want %v", got, want)
		}
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
