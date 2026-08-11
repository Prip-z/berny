import { clearTokens, getAccessToken, getRefreshToken, setTokens } from "../lib/storage/auth";


const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function Fetch(endpoint: string, options: RequestInit = {}): Promise<Response> {
    const token = getAccessToken();

    const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(options.headers as Record<string, string>),
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    let response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        const refreshToken = getRefreshToken();

        if (!refreshToken) {
            clearTokens();
            window.location.href = "/authorization";
            throw new Error("Unauthorized");
        }

        const refreshResponse = await fetch(`${BASE_URL}/identify/api/v1/auth/refresh`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh_token: refreshToken }),
        });

        if (refreshResponse.ok) {
            const data = await refreshResponse.json();
            setTokens(data);

            headers["Authorization"] = `Bearer ${data.tokens.access_token}`;
            response = await fetch(`${BASE_URL}${endpoint}`, {
                ...options,
                headers,
            });
        } else {
            clearTokens();
            window.location.href = "/authorization";
            throw new Error("Session expired");
        }
    }

    return response;
}