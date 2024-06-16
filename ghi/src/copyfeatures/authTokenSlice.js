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
      console.error(state.token)
      const token_data = {
          token: state.token.token,
          token_type: state.token.token_type
      }
      localStorage.setItem('token', JSON.stringify(token_data));
    },
    clearToken: (state) => {
      state.token = null;
      localStorage.removeItem('token');
    }
  }
});

export const { setToken, clearToken } = tokenSlice.actions;
export default tokenSlice.reducer;
