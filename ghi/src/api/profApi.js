import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'


const baseUrl = import.meta.env.VITE_BACKEND_HOST;

if (!baseUrl) {
    console.error('Base URL is not set. Check your environment variables.');
}

export const profApi = createApi({
    reducerPath: 'profApi',
    baseQuery: fetchBaseQuery({
        baseUrl: `${import.meta.env.VITE_BACKEND_HOST}`,
        prepareHeaders: (headers) => {
            const token = JSON.parse(localStorage.getItem('token'))
            if (token) {
                headers.set(
                    'authorization',
                    `${token.token_type} ${token.access_token}`
                );
            }
            return headers;
        }
    }),
    tagTypes: ['User'],
    endpoints: (builder) => ({
        getToken: builder.query({
            query: () => ({
                url: '/token',
                credentials: 'include'
            }),
            providesTags: ['User']
        }),
        login: builder.mutation({
            query: (form) => {
                let formData = new FormData()
                formData.append('username', form.email)
                formData.append('password', form.password)

                return {
                    url: '/token',
                    method: 'POST',
                    credentials: 'include',
                    body: formData
                }
            },
            invalidatesTags: ['User']
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
                }
            },
            invalidatesTags: ['User']
        }),
        updateUser: builder.mutation({
            query: (data) => {
                return {
                    url: '/api/users',
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                    credentials: 'include',
                }
            },
            invalidatesTags: ['User']
        }),
        changePassword: builder.mutation({
            query: (data) => {
                return {
                    url: '/api/users',
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                    credentials: 'include',
                }
            },
            invalidatesTags: ['User'],
        }),
    })
});

export const {
    useLazyGetTokenQuery,
    useLoginMutation,
    useUpdateUserMutation,
    useSignupMutation,
    useChangePasswordMutation,
} = profApi
