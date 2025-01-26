'use client';
import React from 'react';
import type { FormProps } from 'antd';
import { useRouter } from 'next/navigation'
import { Form, Button, Input, notification } from 'antd'

import api from '../../utils/axios';

type FieldType = {
    username?: string;
    password?: string;
    passwordRepeat?: string;
    name?: string;
}




const Register = () => {
    const router = useRouter()
    const [notificationApi, contextHolder] = notification.useNotification();
    const openNotification = (notificationMessage: string) => {
        notificationApi.info({
            message: notificationMessage,
            placement: 'topRight'
        })
    }

    const onFinish: FormProps<FieldType>['onFinish'] = (values) => {
        const registerUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/register`
        const registerData = {'email': values.username, 'password': values.password, 'password_repeat': values.passwordRepeat, 'nick_name': values.name}
        // notificationApi: 一个对象，包含了调用通知相关方法的接口，例如 api.info
        // contextHolder: 一个react组件, 必须放在组件树中，它会渲染一个容器，用于显示通知
        // Context 是 React 的上下文 API（Context API）的一部分，用于在组件树中传递数据，而无需通过 props 一层层地传递。你可以将它理解为一个全局的数据存储容器，里面的值可以被任何组件访问。
        //   const Context = React.createContext({ name: 'Default' });
        api.post(registerUrl, registerData)
        .then((res) => {
          debugger;
            const status_code = res.data.status_code;
            if (status_code === 200){
                router.push('/login')
            } else {
                openNotification(res.data.message)
            }
        })
        console.log('Form Submitted:', values);
    };

  return (
    <div className='flex items-center justify-center h-screen bg-gray-100'>
    <Form onFinish={onFinish}
        labelCol={{ span: 6}}
        wrapperCol={{ span: 14 }}>
      <Form.Item label="邮箱" name="username">
        <Input />
      </Form.Item>
      <Form.Item label="昵称" name="name">
        <Input />
      </Form.Item>
      <Form.Item label="密码" name="password">
        <Input.Password />
      </Form.Item>
      <Form.Item label="重复密码" name="passwordRepeat">
        <Input.Password />
      </Form.Item>
      <Form.Item wrapperCol={{ span: 14, offset: 6}}>
        <Button type="primary" htmlType="submit">
          注册
        </Button>
      </Form.Item>
    </Form>
    {contextHolder}
    </div>
  )
}

export default Register;