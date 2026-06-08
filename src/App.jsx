import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  BadgeCheck,
  Binary,
  FileText,
  Image as ImageIcon,
  KeyRound,
  Lock,
  Network,
  Play,
  RefreshCw,
  ShieldCheck,
  Terminal,
  UnlockKeyhole,
} from "lucide-react";
import "./styles.css";

const tabs = [
  { id: "flow", label: "Project Flow", icon: Activity },
  { id: "hide", label: "Hide Secret", icon: Lock },
  { id: "extract", label: "Extract Secret", icon: UnlockKeyhole },
  { id: "tools", label: "Practical Tools", icon: Terminal },
  { id: "artifacts", label: "Artifacts", icon: FileText },
];

const toolCards = [
  {
    id: "openssl",
    title: "OpenSSL",
    icon: ShieldCheck,
    detail: "Real-world AES, RSA keys, and certificate verification.",
    proves: "Shows how your custom certificate and AES ideas compare to industry command-line crypto.",
  },
  {
    id: "gnupg",
    title: "GnuPG",
    icon: BadgeCheck,
    detail: "Signing, verification, public-key encryption, and private-key decryption.",
    proves: "Adds authenticity: the message can be trusted, not just hidden.",
  },
  {
    id: "password-attack",
    title: "Password Attack",
    icon: Binary,
    detail: "Weak SHA-256 hash cracking with Python, John, and Hashcat concepts.",
    proves: "Demonstrates the attacker mindset and why weak passwords fail.",
  },
  {
    id: "netcat",
    title: "Netcat",
    icon: Network,
    detail: "Transfers ciphertext produced by this project over localhost.",
    proves: "Turns the AES module into a communication demo, not only storage.",
  },
  {
    id: "wireshark",
    title: "Wireshark",
    icon: Activity,
    detail: "Captures localhost traffic and filters on tcp.port == 9999.",
    proves: "Lets the professor see ciphertext on the wire instead of plaintext.",
  },
];

const flowNodes = [
  ["User Input", "Secret text enters the demo."],
  ["Handshake", "Client/server hello and JSON certificate validation."],
  ["Session Key", "Random key material saved to data/session.bin."],
  ["GAN Noise", "GAN output or secure random fallback saved to data/gan_noise.bin."],
  ["AES Crypto", "Final key encrypts the secret into Base64 ciphertext."],
  ["Steganography", "Ciphertext is hidden in data/output.png."],
  ["OTP + Pond", "Access checks prove layered authentication."],
  ["Extraction", "Ciphertext is recovered and decrypted."],
  ["Practical Tools", "OpenSSL, GPG, Netcat, Wireshark, John, and Hashcat connect the demo to real tools."],
];

function api(path, options = {}) {
  return fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  }).then(async (response) => {
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Request failed");
    }
    return data;
  });
}

function StatusPill({ status }) {
  const text = status === "danger" ? "failed" : status || "info";
  return <span className={`pill ${status || "info"}`}>{text}</span>;
}

function StepList({ steps = [] }) {
  if (!steps.length) {
    return <p className="muted">Run a demo to see step-by-step evidence here.</p>;
  }

  return (
    <div className="steps">
      {steps.map((step, index) => (
        <div className="step" key={`${step.label}-${index}`}>
          <div className="stepIndex">{index + 1}</div>
          <div>
            <div className="stepTitle">
              <span>{step.label}</span>
              <StatusPill status={step.status} />
            </div>
            <p>{step.detail}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

function ToolbarButton({ children, icon: Icon = Play, busy, ...props }) {
  return (
    <button className="actionButton" disabled={busy || props.disabled} {...props}>
      {busy ? <RefreshCw className="spin" size={17} /> : <Icon size={17} />}
      <span>{children}</span>
    </button>
  );
}

function ProjectFlow() {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>Project Flow</h2>
          <p>The professor can follow the security story from input to real-world tools.</p>
        </div>
      </div>
      <div className="flowGrid">
        {flowNodes.map(([title, detail], index) => (
          <div className="flowNode" key={title}>
            <div className="flowBadge">{index + 1}</div>
            <h3>{title}</h3>
            <p>{detail}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function HideSecret({ setLog, refreshArtifacts }) {
  const [secret, setSecret] = useState("Professor demo secret message");
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);

  async function runHide() {
    setBusy(true);
    setLog("Running full hide pipeline...");
    try {
      const data = await api("/api/hide", {
        method: "POST",
        body: JSON.stringify({ secret }),
      });
      setResult(data);
      setLog(JSON.stringify(data, null, 2));
      refreshArtifacts();
    } catch (error) {
      setLog(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel splitPanel">
      <div>
        <div className="panelHeader">
          <div>
            <h2>Hide Secret</h2>
            <p>Runs handshake, GAN keying, AES encryption, steganography, OTP, pond auth, and certificate checks.</p>
          </div>
        </div>
        <label className="fieldLabel" htmlFor="secret">Secret message</label>
        <textarea id="secret" value={secret} onChange={(event) => setSecret(event.target.value)} />
        <ToolbarButton icon={Lock} busy={busy} onClick={runHide}>Run Hide Demo</ToolbarButton>
        {result && (
          <div className="metricRow">
            <div className="metric"><span>Attacker score</span><strong>{result.attackerScore}</strong></div>
            <div className="metric"><span>Cipher score</span><strong>{result.cipherAttackScore}</strong></div>
          </div>
        )}
        <StepList steps={result?.steps} />
      </div>
      <div className="previewPanel">
        <div className="previewTitle">
          <ImageIcon size={18} />
          <span>Stego Output</span>
        </div>
        {result?.outputImage ? (
          <img src={`${result.outputImage}?t=${Date.now()}`} alt="Stego output" />
        ) : (
          <div className="emptyPreview">data/output.png appears here after the hide demo.</div>
        )}
        {result?.ciphertextPreview && <pre>{result.ciphertextPreview}</pre>}
      </div>
    </section>
  );
}

function ExtractSecret({ setLog }) {
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);

  async function runExtract() {
    setBusy(true);
    setLog("Running extract pipeline...");
    try {
      const data = await api("/api/extract", { method: "POST", body: "{}" });
      setResult(data);
      setLog(JSON.stringify(data, null, 2));
    } catch (error) {
      setLog(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>Extract Secret</h2>
          <p>Loads saved key material, pulls ciphertext from the stego image, and decrypts the original message.</p>
        </div>
        <ToolbarButton icon={UnlockKeyhole} busy={busy} onClick={runExtract}>Run Extract Demo</ToolbarButton>
      </div>
      {result?.secret && (
        <div className="secretBox">
          <span>Recovered secret</span>
          <strong>{result.secret}</strong>
        </div>
      )}
      <StepList steps={result?.steps} />
    </section>
  );
}

function PracticalTools({ setLog, refreshArtifacts }) {
  const [active, setActive] = useState(null);
  const [busy, setBusy] = useState(null);

  async function runTool(tool) {
    setBusy(tool.id);
    setActive(tool.id);
    setLog(`Running ${tool.title} practical...`);
    try {
      const data = await api(`/api/tools/${tool.id}`, { method: "POST", body: "{}" });
      setLog(data.output || "No output returned.");
      refreshArtifacts();
    } catch (error) {
      setLog(error.message);
    } finally {
      setBusy(null);
    }
  }

  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>Practical Tools</h2>
          <p>Run or explain the external-tool demos that connect your project to real security workflows.</p>
        </div>
      </div>
      <div className="toolGrid">
        {toolCards.map((tool) => {
          const Icon = tool.icon;
          return (
            <article className={`toolCard ${active === tool.id ? "selected" : ""}`} key={tool.id}>
              <div className="toolIcon"><Icon size={22} /></div>
              <h3>{tool.title}</h3>
              <p>{tool.detail}</p>
              <div className="proof">
                <strong>What it proves</strong>
                <span>{tool.proves}</span>
              </div>
              <div className="toolActions">
                <ToolbarButton icon={Play} busy={busy === tool.id} onClick={() => runTool(tool)}>Run Demo</ToolbarButton>
                <button className="ghostButton" onClick={() => setLog(`Artifacts for ${tool.title} are visible in the Artifacts tab after running the demo.`)}>
                  <FileText size={16} />
                  <span>View Files</span>
                </button>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

function Artifacts({ artifacts, refreshArtifacts }) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>Artifacts</h2>
          <p>Files created or used by the core project and practical demos.</p>
        </div>
        <ToolbarButton icon={RefreshCw} onClick={refreshArtifacts}>Refresh</ToolbarButton>
      </div>
      <div className="artifactTable">
        {artifacts.map((item) => (
          <div className="artifactRow" key={item.path}>
            <div>
              <strong>{item.path}</strong>
              <p>{item.purpose}</p>
              {item.preview && <pre>{item.preview}</pre>}
            </div>
            <div className="artifactMeta">
              <StatusPill status={item.exists ? "success" : "danger"} />
              <span>{item.size} bytes</span>
              {item.kind === "image" && item.url && <img src={`${item.url}?t=${Date.now()}`} alt={item.path} />}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function LogPanel({ log }) {
  return (
    <aside className="logPanel">
      <div className="previewTitle">
        <Terminal size={18} />
        <span>Demo Output</span>
      </div>
      <pre>{log || "Run a demo to see backend output, command logs, and generated evidence."}</pre>
    </aside>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState("flow");
  const [status, setStatus] = useState(null);
  const [artifacts, setArtifacts] = useState([]);
  const [log, setLog] = useState("");

  async function refreshArtifacts() {
    const data = await api("/api/artifacts");
    setArtifacts(data.artifacts);
  }

  useEffect(() => {
    api("/api/status")
      .then((data) => {
        setStatus(data);
        setArtifacts(data.artifacts);
        setLog(data.tools);
      })
      .catch((error) => setLog(error.message));
  }, []);

  const activeContent = useMemo(() => {
    if (activeTab === "hide") return <HideSecret setLog={setLog} refreshArtifacts={refreshArtifacts} />;
    if (activeTab === "extract") return <ExtractSecret setLog={setLog} />;
    if (activeTab === "tools") return <PracticalTools setLog={setLog} refreshArtifacts={refreshArtifacts} />;
    if (activeTab === "artifacts") return <Artifacts artifacts={artifacts} refreshArtifacts={refreshArtifacts} />;
    return <ProjectFlow />;
  }, [activeTab, artifacts]);

  return (
    <div className="appShell">
      <header className="topBar">
        <div>
          <h1>Crypto Professor Demo</h1>
          <p>One dashboard for the custom crypto pipeline and practical security tools.</p>
        </div>
        <div className="statusStrip">
          {(status?.modules || []).slice(0, 4).map((module) => (
            <span key={module.name}><KeyRound size={14} /> {module.name}</span>
          ))}
        </div>
      </header>

      <div className="workspace">
        <nav className="sidebar">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button className={activeTab === tab.id ? "active" : ""} key={tab.id} onClick={() => setActiveTab(tab.id)}>
                <Icon size={18} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
        <main>{activeContent}</main>
        <LogPanel log={log} />
      </div>
    </div>
  );
}
