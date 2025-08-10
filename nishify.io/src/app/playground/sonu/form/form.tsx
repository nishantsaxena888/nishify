"use client";

import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { DropdownInput } from "@/components/form/input/dropdown-input";
import { MultiSelectDropdownInput } from "@/components/form/input/multi-select-dropdown-input";

interface FormField {
  id: string;
  type: string;
  label: string;
  placeholder?: string;
  name: string;
  autoComplete?: string;
  required?: boolean;
  list?: any[]; // for dropdowns
  labelBind?: string;
  valueBind?: string;
  searchPlaceholder?: string;
}

interface DynamicFormProps {
  title?: string;
  description?: string;
  fields: FormField[];
  submitText: string;
  redirect?: {
    label: string;
    linkText: string;
    href: string;
  };
  onSubmit?: (
    data: Record<string, any>,
    setErrors: (errors: {
      fieldErrors?: Record<string, string>;
      formError?: string;
    }) => void
  ) => Promise<void> | void;
}

export const DynamicForm = ({
  title = "",
  description = "",
  fields,
  submitText,
  redirect,
  onSubmit,
}: DynamicFormProps) => {
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [formError, setFormError] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    setFormError("");
    setFieldErrors({});

    const formData = new FormData(e.currentTarget);
    const data: Record<string, any> = {};
    fields.forEach((field) => {
      data[field.name] = formData.get(field.name)?.toString() || "";
    });

    const setErrors = ({ fieldErrors = {}, formError = "" }) => {
      setFieldErrors(fieldErrors);
      setFormError(formError);
    };

    try {
      await onSubmit?.(data, setErrors);
    } catch (err: any) {
      setFormError(err?.message || "Something went wrong");
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderField = (field: FormField) => {
    switch (field.type) {
      case "dropdown":
        return (
          <DropdownInput
            list={field.list || []}
            labelBind={field.labelBind || "label"}
            valueBind={field.valueBind || "value"}
            placeholder={field.placeholder || "Select an option"}
            searchPlaceholder={field.searchPlaceholder}
          />
        );
      case "multi-select-dropdown":
        return (
          <MultiSelectDropdownInput
            list={field.list || []}
            labelBind={field.labelBind || "label"}
            valueBind={field.valueBind || "value"}
            placeholder={field.placeholder || "Select options"}
            searchPlaceholder={field.searchPlaceholder}
          />
        );
      default:
        return (
          <Input
            id={field.id}
            name={field.name}
            type={field.type}
            placeholder={field.placeholder}
            autoComplete={field.autoComplete}
            required={field.required}
          />
        );
    }
  };

  return (
    <div className="flex w-full items-center justify-center py-8 lg:py-16">
      <div className="w-full max-w-md space-y-6 px-4">
        {title && <h2 className="text-center text-3xl font-bold">{title}</h2>}
        {description && (
          <p className="text-center text-muted-foreground">{description}</p>
        )}

        {formError && (
          <div className="text-center text-sm text-red-600 font-medium">
            {formError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            {fields.map((field) => (
              <div key={field.id} className="space-y-1">
                <Label htmlFor={field.id}>{field.label}</Label>
                {renderField(field)}
                {fieldErrors[field.name] && (
                  <p className="text-sm text-red-500">
                    {fieldErrors[field.name]}
                  </p>
                )}
              </div>
            ))}
          </div>
          <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting ? "Submitting..." : submitText}
          </Button>
        </form>

        {redirect && (
          <div className="mt-6 text-center text-sm">
            <span className="pr-1">{redirect.label}</span>
            <Link className="underline" href={redirect.href}>
              {redirect.linkText}
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};
