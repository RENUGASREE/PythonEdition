import { Layout } from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useAuth } from "@/hooks/use-auth";
import { useModules } from "@/hooks/use-modules";
import { useQuery } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { useMemo } from "react";
import { Link, useParams } from "wouter";
import { Loader2 } from "lucide-react";

export default function Certificate() {
  const { id } = useParams();
  const moduleId = Number(id);
  const { user } = useAuth();
  const { data: modules, isLoading: loadingModules } = useModules();
  const { data: certificates, isLoading: loadingCertificates } = useQuery({
    queryKey: ["/api/certificates"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/certificates/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (res.status === 401) return [];
      if (!res.ok) throw new Error("Failed to fetch certificates");
      return res.json();
    },
  });

  const module = useMemo(() => {
    return (modules as any[])?.find((m: any) => m.id === moduleId);
  }, [modules, moduleId]);

  const certificate = useMemo(() => {
    if (!module) return null;
    return (certificates || []).find((c: any) => c.module === module.title);
  }, [certificates, module]);

  if (loadingModules || loadingCertificates) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full py-20">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }

  if (!moduleId || !module) {
    return (
      <Layout>
        <div className="max-w-xl mx-auto py-16 px-4 text-center">
          <h1 className="text-2xl font-bold">Certificate not found</h1>
          <p className="text-muted-foreground mt-2">Select a module to view its certificate.</p>
          <Link href="/curriculum">
            <Button className="mt-4">Go to curriculum</Button>
          </Link>
        </div>
      </Layout>
    );
  }

  const issueDate = certificate?.issued_at 
    ? new Date(certificate.issued_at).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) 
    : new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });

  const certId = certificate?.id || `PY-CERT-${module.id}-${user?.id || "DEMO"}-${new Date().getFullYear()}`;
  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=${encodeURIComponent(window.location.href)}`;

  return (
    <Layout>
      <div className="max-w-5xl mx-auto py-12 px-4 space-y-8">
        {/* Certificate Container */}
        <div className="relative bg-white p-1 shadow-2xl overflow-hidden print:shadow-none print:p-0">
          {/* Main Border Wrapper */}
          <div className="border-[12px] border-[#1a2b4b] p-1">
            <div className="border-2 border-[#c5a059] p-12 md:p-16 text-center space-y-10 bg-[#fdfdfd] relative">
              
              {/* Top Header */}
              <div className="flex justify-between items-start">
                <div className="w-24"></div> {/* Spacer */}
                <div className="text-[#1a2b4b] text-2xl font-serif font-semibold tracking-wide">
                  Python Edition
                </div>
                {/* AI Badge */}
                <div className="bg-[#1a2b4b] text-white p-2 text-[10px] font-bold tracking-tighter leading-none border-b-4 border-[#c5a059]">
                  <div className="border border-white/20 p-1">
                    AI VERIFIED LEARNING
                    <div className="text-[#c5a059] mt-0.5">SKILL LEVEL: PRO</div>
                  </div>
                </div>
              </div>

              {/* Title Section */}
              <div className="space-y-4 pt-4">
                <h1 className="text-[#1a2b4b] text-4xl md:text-5xl lg:text-6xl font-serif font-bold tracking-tight uppercase whitespace-nowrap">
                  Certificate of Achievement
                </h1>
                <p className="text-[#666] italic text-lg font-serif">
                  This certification is proudly presented to
                </p>
              </div>

              {/* Recipient Name */}
              <div className="py-6">
                <div className="inline-block border-b-2 border-[#c5a059] pb-2 min-w-[300px]">
                  <span className="text-[#c5a059] text-5xl md:text-6xl font-serif font-medium uppercase tracking-wider px-8">
                    {user?.firstName ? `${user.firstName} ${user.lastName || ""}` : (user?.username || user?.email || "Learner")}
                  </span>
                </div>
              </div>

              {/* Description */}
              <div className="space-y-6 pt-4">
                <p className="text-[#666] text-lg font-serif">
                  For successfully mastering the high-fidelity curriculum of
                </p>
                <h2 className="text-[#1a2b4b] text-3xl md:text-4xl font-serif font-bold tracking-wide">
                  {module.title}
                </h2>
              </div>

              {/* Footer Section */}
              <div className="grid grid-cols-3 items-end pt-12 text-left">
                {/* Left: Signature & Date */}
                <div className="space-y-4">
                  <div className="font-serif italic text-2xl text-[#1a2b4b] border-b border-[#ccc] pb-1 inline-block">
                    Pythonized AI
                  </div>
                  <div className="text-[10px] font-bold text-[#1a2b4b] uppercase tracking-wider">
                    Platform Director, Python Edition
                  </div>
                  <div className="text-xs text-[#666]">
                    Issued on: {issueDate}
                  </div>
                </div>

                {/* Center: QR & ID */}
                <div className="flex flex-col items-center space-y-2">
                  <div className="bg-white p-1 border border-gray-200">
                    <img src={qrUrl} alt="Verification QR Code" className="w-20 h-20" />
                  </div>
                  <div className="text-[8px] text-[#999] uppercase tracking-tighter text-center">
                    Scan to Verify Certificate<br />
                    ID: {certId}
                  </div>
                  <div className="text-[10px] italic text-[#666] font-serif mt-2">
                    Python Edition Adaptive Learning Platform
                  </div>
                </div>

                {/* Right: Verified Seal */}
                <div className="flex justify-end relative">
                  <div className="relative w-32 h-32 flex items-center justify-center">
                    {/* Seal Circular Text */}
                    <div className="absolute inset-0 animate-[spin_20s_linear_infinite]">
                      <svg className="w-full h-full" viewBox="0 0 100 100">
                        {/* Outer Circle Covering everything */}
                        <circle cx="50" cy="50" r="49" fill="none" stroke="#c5a059" strokeWidth="1" />
                        <path id="seal-text-path" d="M 50, 50 m -39, 0 a 39,39 0 1,1 78,0 a 39,39 0 1,1 -78,0" fill="none" />
                        <text className="text-[7px] font-bold fill-[#c5a059] uppercase tracking-[0.2em]">
                          <textPath href="#seal-text-path" startOffset="0">
                            AUTHENTIC • CERTIFIED • PYTHON EDITION • 
                          </textPath>
                        </text>
                      </svg>
                    </div>
                    {/* Seal Inner Circle */}
                    <div className="bg-[#1a2b4b] rounded-full w-20 h-20 flex items-center justify-center border-4 border-[#c5a059] shadow-inner z-10">
                      <div className="text-white font-bold text-sm tracking-tighter border-y border-white/20 py-1 px-2">
                        VERIFIED
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 print:hidden">
          <Link href="/curriculum">
            <Button variant="outline" className="w-full sm:w-auto">
              Back to curriculum
            </Button>
          </Link>
          <div className="flex gap-4 w-full sm:w-auto">
            <Button variant="secondary" className="flex-1 sm:flex-initial" onClick={() => window.print()}>
              Print Certificate
            </Button>
            <Button className="flex-1 sm:flex-initial" onClick={async () => {
              try {
                const accessToken = getAccessToken();
                const response = await fetch(apiUrl(`/certificates/${moduleId}/download/`), {
                  headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
                });
                if (!response.ok) throw new Error("Failed to download certificate");
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `certificate_${user?.username || "learner"}_${moduleId}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
              } catch (err: any) {
                console.error("Download failed:", err);
              }
            }}>
              Download PDF
            </Button>
          </div>
        </div>
        
        {!certificate && (
          <div className="bg-amber-50 border border-amber-200 text-amber-800 p-4 rounded-md text-sm text-center print:hidden">
            Note: This is a preview. Complete all lessons in this module to unlock the official certificate.
          </div>
        )}
      </div>
    </Layout>
  );
}
