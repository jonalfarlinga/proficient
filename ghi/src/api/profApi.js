import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const baseUrl = import.meta.env.VITE_BACKEND_HOST;

if (!baseUrl) {
    console.error('Base URL is not set. Check your environment variables.');
} else {
    console.log('Base URL:', baseUrl);
}

export const profApi = createApi({
    reducerPath: 'profApi',
    baseQuery: fetchBaseQuery({ baseUrl: `${import.meta.env.VITE_BACKEND_HOST}`}),
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
                    credentials: 'include',
                    method: 'POST',
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
                    credentials: 'include',
                }
            },
            invalidatesTags: ['User']
        }),
    })
});

export const {
    useGetTokenQuery,
    useLoginMutation,
    useUpdateUserMutation,
    useSignupMutation,
    useChangePasswordMutation,
} = profApi
