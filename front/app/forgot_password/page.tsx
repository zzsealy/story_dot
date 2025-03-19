'use client';  // 确保这是一个客户端组件
import { useForm, SubmitHandler } from 'react-hook-form';
import React, { useState } from 'react';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';
import api from '../../utils/axios';


import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import Link from 'next/link';

interface FormValues {
  email: string
  ver_code: number
}

const ForgotPasswordForm: React.FC =() => {
    const { register, handleSubmit, formState: { errors }} = useForm<FormValues>();
    const [showVerificationCode, setShowVerificationCode] = useState(false)
    const myOnSubmit: SubmitHandler<FormValues> = (values) => {
      const forgotPasswordUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/forgot_password`
    }

    return (
        <form onSubmit={handleSubmit(myOnSubmit)}>
          <div>
            <Input
              className='bg-gray-100'
              id='email'
              type='email'
              placeholder='邮箱'
              {...register('email', { required: '请输入验证码'})}
            />
          </div> 
          { showVerificationCode && (
            <div>
                <Input
                className='bg-gray-100'
                id='ver_code'
                type='ver_code'
                placeholder='验证码'
                {...register('ver_code', { required: '请输入验证码'})}
                />
            </div> 
          )
          }
          <Button type='submit' className='bg-teal-500 w-full mt-[1vh]'>忘记密码</Button>
        </form>
    )
}

const Login = () => {

  return (
    <div className='flex items-center justify-center h-screen bg-gray-100 flex-col'>
      <div className='flex flex-col w-full max-w-md px-8 pt-6 pb-2 bg-white rounded-lg shadow-md'>
        <h1 className='text-center text-4xl pb-4'>复习册</h1>
        < ForgotPasswordForm />
      </div>
    </div>
  )
}

export default Login;