export function volatilityLabel(std: number): "Low" | "Medium" | "High" {
  if (std < 1.5) return "Low";
  if (std < 3.5) return "Medium";
  return "High";
}
