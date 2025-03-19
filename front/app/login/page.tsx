'use client';  // 确保这是一个客户端组件

import { useForm, SubmitHandler } from 'react-hook-form';
import React from 'react';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';
import api from '../../utils/axios';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import Link from 'next/link';

interface FormValues {
  email: string
  password: string
}

const LoginForm: React.FC = () => {
  const {register, handleSubmit, formState: { errors } } = useForm<FormValues>();
  const router = useRouter()

  const myOnSubmit: SubmitHandler<FormValues> = (values) => {
      const loginUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/login`
      const loginData = {'email': values.email, 'password': values.password}
      api.post(loginUrl, loginData)
      .then((res) => {
          const code = res.data.code;
          if (code === 200) {
              const token = res.data.token;
              localStorage.setItem('story_dot_token', token)
              router.push('/')
          } else if (code >= 500){
            toast(res.data.message)
          } else {
            toast('发生错误')
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
          {...register('email', { required: 'Email is required' })}
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
      <div className='flex flex-col w-full max-w-md px-8 pt-6 pb-2 bg-white rounded-lg shadow-md'>
        <h1 className='text-center text-4xl pb-4'>复习册</h1>
        < LoginForm />
        <div className='mt-4 flex bg-gray-100 w-full h-10 items-center '>
            <Link href='/register'>
              <button type='submit' className='text-gray-500'>注册 </button>
            </Link>
              <span className='text-gray-300'>|</span>
            <Link href='/forgot_password'>            
              <button type='submit' className='text-gray-500'> 忘记密码</button>
            </Link>

        </div>
      </div>
    </div>
  )
}

export default Login;