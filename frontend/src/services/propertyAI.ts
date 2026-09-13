import type {
  PropertyAIResponse,
} from "../types/propertyAI";

export async function askPropertyAI(
  propertyId: number,
  query: string,
): Promise<PropertyAIResponse> {
  const response = await fetch(
    `/api/properties/${propertyId}/ai`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
      }),
    },
  );

  if (!response.ok) {
    const message =
      await response.text();

    throw new Error(
      message ||
        "Unable to analyze property.",
    );
  }

  return response.json() as Promise<PropertyAIResponse>;
}
