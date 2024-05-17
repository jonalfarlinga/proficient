import { useSelector } from 'react-redux'


export const selectToken = (state) => state.token.token;
export const useAuthToken = () => useSelector(selectToken);
