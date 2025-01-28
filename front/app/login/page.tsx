'use client';  // 确保这是一个客户端组件

import { useForm, SubmitHandler } from 'react-hook-form';
import React from 'react';
import { useRouter } from 'next/navigation';
import api from '../../utils/axios';

import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface FormValues {
  email: string
  password: string
}

const LoginForm: React.FC = () => {
  const {register, handleSubmit, formState: { errors } } = useForm<FormValues>();
  const router = useRouter()

  const onSubmit: SubmitHandler<FormValues> = (values) => {

      const loginUrl = `${process.env.NEXT_PUBLIC_API_URL}/users/login`
      const loginData = {'email': values.email, 'password': values.password}
      api.post(loginUrl, loginData)
      .then((res) => {
          const status_code = res.data.status_code;
          if (status_code === 200) {
              const token = res.data.token;
              localStorage.setItem('answer_check', token)
              router.push('/')
          } else {
          }
      })
  }

  return (

    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Label htmlFor="email">邮箱</Label>
        <Input
          id="email"
          type="email"
          {...register('email', { required: 'Password is required' })}
        />
        {errors.email && <span className="text-red-500">{errors.email.message}</span>}
      </div>
      <div>
        <Label htmlFor="password">密码</Label>
        <Input
          id="password"
          type="password"
          {...register('password', { required: 'Password is required' })}
        />
        {errors.password && <span className="text-red-500">{errors.password.message}</span>}
      </div>

      <Button type='submit'>登录</Button>
    </form>
  )


}

const Login = () => {

  return (
    <div className='flex items-center justify-center h-screen bg-gray-100'>
    < LoginForm />
    </div>
  )
}

export default Login;