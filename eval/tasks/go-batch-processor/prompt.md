Write a Go file `solution.go` in `package solution` (standard library only).

Implement exactly this exported function:

```go
func ProcessBatches(items []int, batchSize int, fn func([]int) (int, error)) ([]int, error)
```

Behaviour:

1. Split `items` into consecutive batches of at most `batchSize`. The final
   batch may be shorter.
2. Process every batch **concurrently**, each in its own goroutine.
3. Return one result per batch, in batch order — not in completion order.
4. If any batches fail, return the results slice alongside a single error that
   combines every batch error, so a caller can still match against each one.
5. `batchSize <= 0` or empty `items` returns an empty result and a nil error.

The module targets Go 1.27. Return only the contents of `solution.go` in a
single Go code block.
