import { setToken, clearToken } from '/src/features/authTokenSlice'


export const authMiddleware = (store) => (next) => (action) => {
    if (action.type.endsWith('/fulfilled') && action.payload.token) {
        store.dispatch(setToken(action.payload.token))
    }
    if (action.type.endsWith('/rejected')) {
        store.dispatch(clearToken());
    }
    return next(action)
};
