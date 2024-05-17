import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import { profApi } from './api/profApi'
import tokenReducer from '/src/features/authTokenSlice'
import { authMiddleware } from '/src/middleware/authMiddleware'

export const store = configureStore({
    reducer: {
        [profApi.reducerPath]: profApi.reducer,
        token: tokenReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(profApi.middleware, authMiddleware),
})

setupListeners(store.dispatch)
