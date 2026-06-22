import { confidenceClass, type ConfidenceGrade } from "@/lib/confidence";

export function ConfidenceBadge({ grade }: { grade: ConfidenceGrade }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${confidenceClass(grade)}`}>
      {grade}
    </span>
  );
}
