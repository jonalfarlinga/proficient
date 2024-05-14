import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import { profApi } from './redux/profApi'

export const store = configureStore({
    reducer: {
        [profApi.reducerPath]: profApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(profApi.middleware),
})

setupListeners(store.dispatch)
