/**
 * Loading Spinner Component
 */
interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  message?: string;
}

export function LoadingSpinner({ size = "md", message }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: "w-6 h-6",
    md: "w-10 h-10",
    lg: "w-16 h-16",
  };

  return (
    <div className="flex flex-col items-center justify-center gap-3">
      <div
        className={`${sizeClasses[size]} border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin`}
      />
      {message && (
        <p className="text-gray-400 text-sm animate-pulse">{message}</p>
      )}
    </div>
  );
}

/**
 * Skeleton loader for cards
 */
export function CardSkeleton() {
  return (
    <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 animate-pulse">
      <div className="h-4 bg-slate-700 rounded w-1/2 mb-3" />
      <div className="h-8 bg-slate-700 rounded w-3/4" />
    </div>
  );
}

/**
 * Skeleton loader for graphs
 */
export function GraphSkeleton() {
  return (
    <div className="bg-slate-900/50 rounded-xl p-4 animate-pulse">
      <div className="h-6 bg-slate-700 rounded w-1/3 mb-4" />
      <div className="h-64 bg-slate-800 rounded flex items-end justify-around p-4 gap-2">
        {[...Array(12)].map((_, i) => (
          <div
            key={i}
            className="bg-slate-700 rounded-t w-full"
            style={{ height: `${Math.random() * 60 + 20}%` }}
          />
        ))}
      </div>
    </div>
  );
}
