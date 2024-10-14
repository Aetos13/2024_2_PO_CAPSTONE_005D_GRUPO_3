import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const login = (email, password) => {
    return axios.post(`${API_URL}/login`, { email, password });
};

export const register = (userData) => {
    return axios.post(`${API_URL}/register`, userData);
};

export const resetPassword = (email) => {
    return axios.post(`${API_URL}/reset_password`, { email });
};