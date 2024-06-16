import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  token: null,
};

const tokenSlice = createSlice({
  name: 'token',
  initialState,
  reducers: {
    setToken: (state, action) => {
      state.token = action.payload;
      const local_token = {
        access_token: action.payload.access_token,
        token_type: action.payload.token_type
    }
      localStorage.setItem('token', JSON.stringify(local_token));
    },
    clearToken: (state) => {
      state.token = null;
      localStorage.removeItem('token');
    }
  }
});

export const { setToken, clearToken } = tokenSlice.actions;
export default tokenSlice.reducer;
