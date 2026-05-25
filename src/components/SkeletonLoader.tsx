export function SkeletonLoader() {
  return (
    <div className="rounded-xl border border-border/30 p-5 w-full bg-secondary/5">
      <div className="mb-4 flex items-center justify-between">
        <div className="h-3 w-16 animate-pulse rounded-md bg-secondary/80"></div>
      </div>
      <div className="mb-3 h-5 w-3/4 animate-pulse rounded-md bg-secondary/60"></div>
      <div className="mb-2 h-4 w-full animate-pulse rounded-md bg-secondary/40"></div>
      <div className="mb-6 h-4 w-5/6 animate-pulse rounded-md bg-secondary/40"></div>
      
      <div className="mt-auto flex items-center justify-between pt-2">
        <div className="h-3 w-12 animate-pulse rounded-md bg-secondary/30"></div>
        <div className="h-3 w-8 animate-pulse rounded-md bg-secondary/30"></div>
      </div>
    </div>
  );
}

export function SkeletonGrid({ count = 3 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonLoader key={i} />
      ))}
    </div>
  );
}
