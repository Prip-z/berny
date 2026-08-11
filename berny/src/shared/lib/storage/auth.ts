export function getAccessToken() {
    const token = localStorage.getItem('accessToken')
    return token
}

export function getRefreshToken() {
    const token = localStorage.getItem('refreshToken')
    return token
}

export function setTokens(data: any) {
    localStorage.setItem("accessToken", data.tokens.access_token);
    localStorage.setItem("refreshToken", data.tokens.refresh_token);
}

export function clearTokens() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
}