import React from 'react';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const faqData = [
  {
    question: "Is this legal advice?",
    answer: "No. This application is not a substitute for legal advice. It is a tool to help you organize and document your digital assets. You should always consult with a qualified attorney regarding your estate plan."
  },
  {
    question: "How is my data stored? Is it secure?",
    answer: "This is a client-side only application. No data you enter is ever sent to a server or stored by us. All information is processed in your browser. The 'Save Draft' feature uses your browser's local storage, which is private to your computer and your browser profile."
  },
  {
    question: "Why shouldn't I enter my private keys or seed phrases?",
    answer: "Your private keys and seed phrases grant complete control over your crypto assets. Entering them into any online application, including this one, is extremely risky. You should store them in a secure, offline location (e.g., a hardware wallet, a metal seed plate, or a safe) and only share their location with your trusted executor."
  },
  {
    question: "How does this tool comply with estate laws?",
    answer: "This tool is designed to create an addendum that is compliant with the Revised Uniform Fiduciary Access to Digital Assets Act (RUFADAA) and the Uniform Probate Code. It helps ensure your executor has the legal standing to access and manage your digital assets as intended."
  },
  {
    question: "What are the tax implications of cryptocurrency inheritance?",
    answer: "In the U.S., cryptocurrencies are treated as property by the IRS. When inherited, they typically receive a 'step-up' in cost basis to their fair market value on the date of death. The federal estate tax exemption is quite high (over $13 million per individual in 2025), so most estates will not owe federal estate tax. However, state laws vary. Please consult a tax professional."
  },
];

const FaqPage = () => {
  return (
    <div className="container mx-auto py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Legal & Frequently Asked Questions</h1>
      </div>

      <div className="max-w-4xl mx-auto">
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Legal Disclaimer</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-gray-300">
            <p><strong>Not Legal Advice:</strong> The information and documents provided by LastWish.eth are for informational purposes only and do not constitute legal advice. We are not a law firm.</p>
            <p><strong>Consult an Attorney:</strong> Using this service does not create an attorney-client relationship. You should consult with a qualified legal professional to address your specific situation and to ensure your estate plan is valid and enforceable in your jurisdiction.</p>
            <p><strong>Compliance:</strong> This tool is designed to help you create a document that complies with the Revised Uniform Fiduciary Access to Digital Assets Act (RUFADAA) and the Uniform Probate Code, but laws vary by state and are subject to change.</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Frequently Asked Questions</CardTitle>
          </CardHeader>
          <CardContent>
            <Accordion type="single" collapsible className="w-full">
              {faqData.map((faq, index) => (
                <AccordionItem value={`item-${index}`} key={index}>
                  <AccordionTrigger>{faq.question}</AccordionTrigger>
                  <AccordionContent>
                    {faq.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default FaqPage;
