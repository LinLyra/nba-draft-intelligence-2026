export type ConfidenceGrade = "A+" | "A" | "B+" | "B" | "C+" | "C" | "D";

export function confidenceScore(
  probability: number,
  stdPick: number,
  sourceCount: number
): number {
  const probPart = probability * 45;
  const sourcePart = Math.min(sourceCount / 8, 1) * 25;
  const volPart = Math.max(0, 30 - stdPick * 8);
  return probPart + sourcePart + volPart;
}

export function confidenceGrade(
  probability: number,
  stdPick = 2,
  sourceCount = 5
): ConfidenceGrade {
  const score = confidenceScore(probability, stdPick, sourceCount);
  if (score >= 92) return "A+";
  if (score >= 85) return "A";
  if (score >= 75) return "B+";
  if (score >= 65) return "B";
  if (score >= 55) return "C+";
  if (score >= 45) return "C";
  return "D";
}

export function confidenceClass(grade: ConfidenceGrade): string {
  if (grade.startsWith("A")) return "text-emerald-300 bg-emerald-500/15";
  if (grade.startsWith("B")) return "text-amber-300 bg-amber-500/15";
  if (grade.startsWith("C")) return "text-orange-300 bg-orange-500/15";
  return "text-rose-300 bg-rose-500/15";
}
