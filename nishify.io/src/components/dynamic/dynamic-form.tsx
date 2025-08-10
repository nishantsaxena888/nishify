/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useMemo } from "react";
import { DynamicForm } from "@/components/form/form";

// ✅ Statically import known form configs
import formLogin from "@/clients/pioneer_wholesale_inc/forms/form-login.json";
import formRegister from "@/clients/pioneer_wholesale_inc/forms/form-register.json";
import formForgotPassword from "@/clients/pioneer_wholesale_inc/forms/form-forgot-password.json";

const formConfigs: Record<string, any> = {
  login: formLogin,
  register: formRegister,
  "forgot-password": formForgotPassword,
};

export default function DynamicFormRenderer({ type }: { type?: string }) {
  const formType = (type?.replace("form:", "") || "login").replace("-form", "");
  const config = useMemo(() => formConfigs[formType], [formType]);

  if (!config)
    return (
      <div className="text-red-500">
        ❌ Unknown form type: <strong>{formType}</strong>
      </div>
    );

  return (
    <DynamicForm
      title={config.title}
      description={config.description}
      fields={config.fields}
      submitText={config.submitText}
      redirect={config.redirect}
      onSubmit={config.onSubmit}
    />
  );
}
