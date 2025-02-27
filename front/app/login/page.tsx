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

  const myOnSubmit: SubmitHandler<FormValues> = (values) => {

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

    <form onSubmit={handleSubmit(myOnSubmit)} className="space-y-4">
      <div>
        {/* <Label htmlFor="email">邮箱</Label> */}
        <Input
          className='bg-gray-100'
          id="email"
          type="email"
          placeholder='邮箱'
          {...register('email', { required: 'Password is required' })}
        />
        {errors.email && <span className="text-red-500">{errors.email.message}</span>}
      </div>
      <div>
        {/* <Label htmlFor="password">密码</Label> */}
        <Input
          className='bg-gray-100'
          id="password"
          type="password"
          placeholder='密码'
          {...register('password', { required: 'Password is required' })}
        />
        {errors.password && <span className="text-red-500">{errors.password.message}</span>}
      </div>

      <Button type='submit' className='bg-teal-500 w-full'>登录</Button>
    </form>
  )


}

const Login = () => {

  return (
    <div className='flex items-center justify-center h-screen bg-gray-100 flex-col'>
      <div className='flex flex-col w-full max-w-md px-8 pt-6 pb-2 bg-white rounded-lg shadow-md h-[36vh]'>
        <h1 className='text-center text-4xl pb-4'>复习册</h1>
        {/* <div className='mb-4'>
          <CaptchaForm />
        </div> */}
        <div className="flex-grow">
          < LoginForm />
        </div>
        <div className='flex bg-gray-100 w-full h-10 mt-auto items-center'>
            <text type='submit' className='text-gray-500'>注册 </text>
            <text className='text-gray-300'>|</text>
            <text type='submit' className='text-gray-500'> 忘记密码</text>
        </div>
      </div>
    </div>
  )
}

export default Login;