"use client";

import { useState } from "react";
import { FileUploadComponent } from "../components/FileUploadComponent";
import Image from "next/image";
import { toast } from "sonner";

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);

  const handleFilesSelected = (newFiles: File[]) => {
    setFiles(newFiles);
  };

  const sendFilesToServer = async (files: File[]) => {
    const formData = new FormData();

    files.forEach((file) => {
      formData.append("file", file);
    });

    try {
      const response = await fetch("http://localhost:5000/csv", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        toast.success("Fichiers envoyés avec succès");
      } else {
        toast.error("Erreur lors de l'envoie des fichiers");
        console.error("Erreur lors de l'envoi des fichiers", response);
      }
    } catch (error) {
      console.error("Erreur de réseau", error);
    }
  };

  // Gestionnaire de clic pour lancer le processus
  const handleProcessStart = () => {
    if (files.length === 0) {
      alert(
        "Veuillez sélectionner des fichiers CSV avant de lancer le processus."
      );
      return;
    }

    sendFilesToServer(files);
  };

  return (
    <div className="flex flex-col justify-center items-center p-8 pb-20 gap-2 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <FileUploadComponent onFilesSelected={handleFilesSelected} />

        <div className="flex gap-2 items-center flex-col justify-center w-full sm:flex-row">
          <button
            onClick={handleProcessStart} // Lancer le processus lorsqu'on clique sur ce bouton
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={20}
              height={20}
            />
            Lancer le processus
          </button>
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 mt-10 flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="http://localhost:8080/login"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/window.svg"
            alt="Window icon"
            width={16}
            height={16}
          />
          Accéder à l'UI Airflow
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="http://localhost:9870/"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          Accéder à l'interface HDFS
        </a>
      </footer>
    </div>
  );
}
