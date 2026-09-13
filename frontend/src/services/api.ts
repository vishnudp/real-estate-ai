const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface PropertyMetadata {
  record_id?:any
  property_id?: number | string;
  property_name?: string;
  developer?: string;
  brand?: string;
  country?: string;
  city?: string;
  location?: string;
  property_type?: string;
  investment_type?: string;
  description?: string;
  source_url?: string;
  price?: string;
  bedrooms?: string;
  area?: string;
  title?: string;
  
}

export interface PropertyResult {
  id?: number;
  property_id?: number | null;

  record_id?: string | null;

  chroma_id?: string | null;
  document: string;
  metadata: PropertyMetadata;
  
}

export interface PropertySearchResponse {
  query: string;
  results: PropertyResult[];
}

export async function getHealth() {
  const response = await fetch(`${API_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend unavailable");
  }

  return response.json();
}

export async function getProperties(params = "") {
  const response = await fetch(
    `${API_URL}/api/properties${params}`
  );

  if (!response.ok) {
    throw new Error("Unable to fetch properties");
  }

  return response.json();
}

export async function searchProperties(
  query: string,
  limit = 20
): Promise<PropertySearchResponse> {
  const response = await fetch(
    `${API_URL}/api/search?q=${encodeURIComponent(
      query
    )}&limit=${limit}`
  );

  if (!response.ok) {
    throw new Error("Unable to search properties");
  }

  return response.json();
}

export async function searchKnowledge(query: string) {
  const response = await fetch(
    `${API_URL}/api/search?q=${encodeURIComponent(query)}`
  );

  if (!response.ok) {
    throw new Error("Unable to search knowledge base");
  }

  return response.json();
}

export async function chat(query: string) {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: query,
    }),
  });

  if (!response.ok) {
    throw new Error("Unable to connect to chat service");
  }

  return response.json();
}

export async function askPropertyAI(
  propertyId: number,
  query: string
) {
  const response = await fetch(
    `${API_URL}/api/properties/${propertyId}/ai`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
      }),
    }
  );

  if (!response.ok) {
    const message = await response.text();

    throw new Error(
      message || "Unable to analyze property."
    );
  }

  return response.json();
}
