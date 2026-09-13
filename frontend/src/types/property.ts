export interface Property {
  id: number;
  source: string;
  external_id?: string;

  title: string;
  project_name?: string;
  developer?: string;

  listing_type?: string;
  property_type?: string;

  country?: string;
  city?: string;
  location?: string;

  price?: number;
  currency?: string;

  bedrooms?: number;
  bathrooms?: number;

  area?: number;
  area_unit?: string;

  status?: string;
  completion_date?: string;

  description?: string;

  amenities?: string[];
  brands?: string[];
  images?: string[];

  source_url: string;
}

export interface PropertyMetadata {
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

export interface PropertyIntelligence {
  summary: string;

  strengths: string[];

  risks: string[];

  infrastructure: {
    score: number;
    assessment: string;
    strengths: string[];
    weaknesses: string[];
  };

  pricing: {
    available: boolean;
    comparable_count: number;
    priced_comparables: number;
    average_price?: number;
    median_price?: number;
    average_price_per_area?: number;
  };

  data_completeness: number;

  confidence: number;
}

export interface PropertyAnalysis {
  property_id: number;
  intelligence: PropertyIntelligence;
}

export interface PropertyResult {
  id?: number;
  document: string;
  metadata: PropertyMetadata;
}
