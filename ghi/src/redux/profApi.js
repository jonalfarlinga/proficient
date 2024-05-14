import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const profApi = createApi({
    reducerPath: 'profApi',
    baseQuery: fetchBaseQuery({ baseUrl: `${import.meta.env.BACKEND_HOST}`}),
    tagTypes: ['User'],
    endpoints: (builder) => ({
        getToken: builder.query({
            query: () => ({
                url: "/token",
                credentials: 'include',
            }),
            providesTags: ['User']
        }),
        login: builder.mutation({
            query: (data) => ({
                url: `/token`,
                method: 'POST',
                params: {
                    username: data.email,
                    password: data.password
                },
                credentials: 'include'
            }),
            invalidatesTags: ['User'],
        }),
        logout: builder.mutation({
            query: () => ({
                url: '/token',
                method: 'DELETE',
                credentials: 'include',
            }),
            invalidatesTags: ['User'],
        }),
        signup: builder.mutation({
            query: (data) => {
                return {
                    url: '/api/users',
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                    credentials: 'include',
                }
            },
            invalidatesTags: ['User']
        })
    })
})


export const {
    useGetTokenQuery,
    useLoginMutation,
    useLogoutMutation,
    useSignupMutation,
} = profApi
