from dataclasses import dataclass

@dataclass
class SecurityDecision:
    action: str
    reason: str

def evaluate_event(category: str, authorized: bool, severity: int) -> SecurityDecision:
    if not authorized:
        return SecurityDecision("BLOCK", "Action is outside authorized scope")
    if severity >= 7:
        return SecurityDecision("REVIEW", "High severity event requires human review")
    return SecurityDecision("ALLOW", "Within authorized policy")

def answer(prompt: str) -> str:
    p = prompt.lower()
    if "package" in p or ".obs" in p:
        return "Use obs init, obs build and obs inspect. Packages are experimental and require verification."
    if "security" in p:
        return "EDEN security policy is local-first. High-impact actions require authorization and review."
    return "EDEN AI model inference is not configured. This local assistant currently provides help and policy guidance."
