export const API_ENDPOINT : string = import.meta.env.DEV ? `http://${window.location.hostname}:8000/api/v1` : '/api/v1';
