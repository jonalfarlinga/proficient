import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  token: JSON.parse(localStorage.getItem('user')) || null,
};

const tokenSlice = createSlice({
  name: 'token',
  initialState,
  reducers: {
    setToken: (state, action) => {
      state.token = action.payload;
      localStorage.setItem('user', JSON.stringify(action.payload));
    },
    clearToken: (state) => {
      state.token = null;
      localStorage.removeItem('user');
    }
  }
});

export const { setToken, clearToken } = tokenSlice.actions;
export default tokenSlice.reducer;
