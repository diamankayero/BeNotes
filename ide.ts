import { useState } from "react";
import { loadPyodide } from "pyodide";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export default function PythonNotebook() {
  const [code, setCode] = useState("print('Hello, world!')");
  const [output, setOutput] = useState("");
  const [pyodide, setPyodide] = useState(null);

  async function initPyodide() {
    if (!pyodide) {
      const py = await loadPyodide();
      setPyodide(py);
    }
  }

  async function runCode() {
    await initPyodide();
    try {
      const result = pyodide.runPython(code);
      setOutput(result);
    } catch (error) {
      setOutput(error.message);
    }
  }

  return (
    <div className="p-4 max-w-2xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Python Notebook</h1>
      <Textarea
        className="h-40 w-full font-mono"
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
      <Button onClick={runCode}>Exécuter</Button>
      <pre className="bg-gray-800 text-white p-4 rounded-xl min-h-[50px]">
        {output}
      </pre>
    </div>
  );
}
