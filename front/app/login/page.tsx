'use client';  // 确保这是一个客户端组件

import React from 'react';
import type { FormProps } from 'antd';
import { useRouter } from 'next/navigation';
import { Form, Button, Input, notification } from 'antd'
import api from '../../utils/axios';

type FieldType = {
    username?: string;
    password?: string;
    remember?: string;
}


const Login = () => {
    const [notificationApi, contextHolder] = notification.useNotification();
    const openNotification = (notificationMessage: string) => {
        notificationApi.info({
            message: notificationMessage,
            placement: 'topRight'
        })
      }
    const router = useRouter()
    const onFinish: FormProps<FieldType>['onFinish'] = (values) => {
      const loginUrl = `${process.env.NEXT_PUBLIC_API_URL}/users/login`
      const loginData = {'email': values.username, 'password': values.password}
      debugger;
      api.post(loginUrl, loginData)
      .then((res) => {
          const status_code = res.data.status_code;
          if (status_code === 200) {
              const token = res.data.token;
              localStorage.setItem('answer_check', token)
              router.push('/')
              openNotification('登录成功')
          } else {
              openNotification(res.data.message)
          }
      })
      console.log('Form Submitted:', values);
    };

  return (
    <div className='flex items-center justify-center h-screen bg-gray-100'>
    <Form onFinish={onFinish}>
      <Form.Item label="邮箱" name="username">
        <Input />
      </Form.Item>
      <Form.Item label="密码" name="password">
        <Input.Password />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          登录
        </Button>
      </Form.Item>
    </Form>
    {contextHolder}
    </div>
  )
}

export default Login;