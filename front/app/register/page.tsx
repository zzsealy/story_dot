'use client';
import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { useRouter } from 'next/navigation'
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
// import CaptchaForm from '../components/captchaForm';


import api from '../../utils/axios';

interface FormValues {
  email: string;
  password: string;
  repeat_password: string;
  ver_code: number;
}

const RegisterForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>();
  const [showVerificationCode, setShowverificationCode] = useState(false)
  const router = useRouter()

  const myOnSubmit: SubmitHandler<FormValues> = (values) => {
    if(!showVerificationCode){
      const sendEmailUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/send_email_code`
      api.post(sendEmailUrl, {'email': values.email})
        .then((res) => {
          const status_code = res.data.status_code
          if(status_code === 200){
            setShowverificationCode(true)
          } else if(status_code >= 500){
            toast(res.data.message)
          }
        })
    } else {
      const registerUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/register`
      const registerData = {'email': values.email, 'password': values.password, 'password_repeat': values.repeat_password, 'ver_code': values.ver_code}
      // notificationApi: 一个对象，包含了调用通知相关方法的接口，例如 api.info
      // contextHolder: 一个react组件, 必须放在组件树中，它会渲染一个容器，用于显示通知
      // Context 是 React 的上下文 API（Context API）的一部分，用于在组件树中传递数据，而无需通过 props 一层层地传递。你可以将它理解为一个全局的数据存储容器，里面的值可以被任何组件访问。
      //   const Context = React.createContext({ name: 'Default' });
      api.post(registerUrl, registerData)
      .then((res) => {
          const status_code = res.data.status_code;
          if (status_code === 200){
              router.push('/login')
          } else {
            toast(res.data.message)
          }
      })
      console.log('Form Submitted:', values);

    }
  };

  return (
    <form onSubmit={handleSubmit(myOnSubmit)} className="space-y-4">
      {/* <div>
        <Label htmlFor="nick_name">昵称</Label>
        <Input
          id="nick_name"
          {...register('nick_name', { required: 'Username is required' })}
        />
        {errors.nick_name && <span className="text-red-500">{errors.nick_name.message}</span>}
      </div> */}

      <div>
        <Label htmlFor="email">邮箱</Label>
        <Input
          id="email"
          type="email"
          {...register('email', { required: '请输入邮箱' })}
        />
        {errors.email && <span className="text-red-500">{errors.email.message}</span>}
      </div>

      <div>
        <Label htmlFor="password">密码</Label>
        <Input
          id="password"
          type="password"
          {...register('password', { required: '请输入密码' })}
        />
        {errors.password && <span className="text-red-500">{errors.password.message}</span>}
      </div>
      <div>
        <Label htmlFor="password">重复密码</Label>
        <Input
          id="password"
          type="password"
          {...register('repeat_password', { required: '请输入密码' })}
        />
        {errors.repeat_password && <span className="text-red-500">{errors.repeat_password.message}</span>}
      </div>
      { showVerificationCode && (
        <div>
          <Label htmlFor="password">邮箱验证码</Label>
          <Input
            id="ver_code"
            {...register('ver_code', { required: '请输入邮箱验证码' })}
          />
          {errors.repeat_password && <span className="text-red-500">{errors.repeat_password.message}</span>}
        </div>
        )
      }

      <Button type="submit" className='bg-green-400'>{ showVerificationCode ? '注册' : '获取验证码'}</Button>
    </form>
  );
};



const Register = () => {

  return (
    <div className='flex items-center justify-center h-screen bg-gray-100 flex-col'>
      <div className='flex flex-col space-y-4 w-full max-w-md px-8 py-6 bg-white rounded-lg shadow-md'>

      {/* <div className='mb-4'>
        <CaptchaForm />
      </div> */}
      <RegisterForm />
      </div>
    </div>
  )
}

export default Register;