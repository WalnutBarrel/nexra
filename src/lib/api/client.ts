const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export class ApiClient {
  static async fetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultHeaders = {
      "Content-Type": "application/json",
      "Accept": "application/json",
    };

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    const response = await fetch(url, config);
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    
    return response.json();
  }
}

export const IntelligenceApi = {
  search: (query: string) => ApiClient.fetch(`/search?q=${encodeURIComponent(query)}`),
  getNews: () => ApiClient.fetch(`/news`),
  getWebsites: () => ApiClient.fetch(`/websites`),
  scanWebsite: (domain: string) => ApiClient.fetch(`/websites/scan/${encodeURIComponent(domain)}`),
};

export const AdminApi = {
  getMetrics: () => ApiClient.fetch(`/admin/metrics`),
  getAnalytics: () => ApiClient.fetch(`/analytics`),
};

export const WorkspaceApi = {
  queryDossier: (query: string, context: any) => ApiClient.fetch(`/ai/query`, {
    method: "POST",
    body: JSON.stringify({ query, context })
  }),
  generateNarrative: (dossier: any) => ApiClient.fetch(`/ai/narrate`, {
    method: "POST",
    body: JSON.stringify({ dossier })
  }),
  exportMarkdown: (dossier: any) => ApiClient.fetch(`/ai/export/markdown`, {
    method: "POST",
    body: JSON.stringify({ dossier })
  }),
};

export const AuthApi = {
  login: (credentials: any) => ApiClient.fetch(`/auth/login`, {
    method: "POST",
    body: JSON.stringify(credentials)
  }),
  getMe: () => ApiClient.fetch(`/auth/me`)
};


