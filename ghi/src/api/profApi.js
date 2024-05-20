import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { setToken, clearToken } from '/src/features/authTokenSlice'

export const profApi = createApi({
    reducerPath: 'profApi',
    baseQuery: fetchBaseQuery({ baseUrl: `${import.meta.env.VITE_BACKEND_HOST}`}),
    tagTypes: ['User'],
    endpoints: (builder) => ({
        getToken: builder.query({
            query: () => {
                var token
                try {
                    token = JSON.parse(localStorage.getItem('user'));
                    token = `${token.token_type} ${token.access_token}`;
                } catch {
                    token = "";
                }
                return {
                    url: "/token",
                    headers: {
                        "authorization": token
                    }
                }
            },
            providesTags: ['User'],
            async onQueryStarted(arg, { dispatch, queryFulfilled }) {
                try {
                    const { data } = await queryFulfilled;
                    dispatch(setToken(data.token));
                } catch {
                    dispatch(clearToken());
                }
            }

        }),
        login: builder.mutation({
            query: (data) => {
                let formData = new FormData()
                formData.append('username', data.email)
                formData.append('password', data.password)
                return {
                    url: `/token`,
                    method: 'POST',
                    body: formData,
                    credentials: 'include'
                }
            },
            invalidatesTags: ['User'],
            async onQueryStarted(arg, { dispatch, queryFulfilled }) {
                try {
                    const { data } = await queryFulfilled;
                    localStorage.setItem('user', JSON.stringify(data));
                    setToken(data)
                } catch {
                    dispatch(clearToken())
                }
            }
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
            invalidatesTags: ['User'],
            async onQueryStarted(arg, { dispatch, queryFulfilled }) {
                try {
                    const { data } = await queryFulfilled;
                    localStorage.setItem('user', JSON.stringify(data));
                    setToken(data)
                } catch {
                    dispatch(clearToken())
                }
            }
        }),
        updateUser: builder.mutation({
            query: (data) => {
                return {
                    url: '/api/users',
                    method: 'UPDATE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                    credentials: 'include',
                }
            },
            invalidatesTags: ['User'],
            async onQueryStarted(arg, { dispatch, queryFulfilled }) {
                try {
                    const { data } = await queryFulfilled;
                    localStorage.setItem('user', JSON.stringify(data));
                    setToken(data)
                } catch {
                    dispatch(clearToken())
                }
            }
        }),
        changePassword: builder.mutation({
            query: (data) => {
                return {
                    url: '/api/users',
                    method: 'UPDATE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                    credentials: 'include',
                }
            },
            invalidatesTags: ['User'],
            async onQueryStarted(arg, { dispatch, queryFulfilled }) {
                try {
                    const { data } = await queryFulfilled;
                    localStorage.setItem('user', JSON.stringify(data));
                    setToken(data)
                } catch {
                    dispatch(clearToken())
                }
            }
        })
    })
})


export const {
    useGetTokenQuery,
    useLoginMutation,
    useUpdateUserMutation,
    useSignupMutation,
    useChangePasswordMutation,
} = profApi
