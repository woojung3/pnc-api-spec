/**
 * KPNC (Korea PnC) PKI API Spectral Ruleset
 * Adds National Infrastructure Overrides
 */
export default {
  rules: {
    /* 1. KPNC Header Convention: Prefix 'KPNC-' + Pascal-Kebab-Case */
    // KPNC 헤더 규칙을 정의합니다.
    "kpnc-header-convention": {
      description: "Custom headers must start with 'KPNC-' and follow Pascal-Kebab-Case (e.g., KPNC-From-Party-Id).",
      message: "Header '{{property}}' does not follow KPNC convention (KPNC-Pascal-Kebab-Case).",
      severity: "error",
      given: "$.components.parameters[?(@.in === 'header')].name",
      then: {
        function: "pattern",
        functionOptions: {
          match: "^KPNC-([A-Z][a-z0-9]+(-[A-Z][a-z0-9]+)*)$"
        }
      }
    },

    /* 2. Path Convention: Lowercase kebab-case */
    "path-kebab-case": {
      description: "URL paths must be in lowercase kebab-case.",
      message: "{{property}} is not lowercase kebab-case.",
      severity: "error",
      resolved: false,
      given: "$.paths[*]~",
      then: {
        function: "pattern",
        functionOptions: {
          match: "^(/([a-z0-9-]+|\\{[a-zA-Z][a-zA-Z0-9]*\\}))+$"
        }
      }
    },

    /* 3. Mandatory Security: Every operation must have security defined */
    "mandatory-security": {
      description: "Every operation must have at least one security requirement (e.g., OAuth2 or mTLS).",
      message: "Operation {{path}} is missing security definitions.",
      severity: "error",
      given: "$.paths[*][get,post,put,delete]",
      then: {
        field: "security",
        function: "truthy"
      }
    },

    /* 4. Standard Error Response: Must ref one of the common error responses */
    "standard-error-response": {
      description: "Error responses (4xx, 5xx) must reference a standard ProblemDetail response.",
      message: "Error response {{path}} should reference a standard error response (e.g., BadRequest, Unauthorized).",
      severity: "warn",
      given: "$.paths[*][*].responses[?(@property >= 400)]",
      then: {
        field: "$ref",
        function: "pattern",
        functionOptions: {
          match: "(BadRequest|Unauthorized|Forbidden|NotFound|Conflict|TooManyRequests|InternalServerError|ProblemDetailResponse)$"
        }
      }
    },

    /* 5. Redocly Optimization: Operations must have summary and description */
    "operation-description-required": {
      description: "Operations must have a summary and description for professional documentation.",
      severity: "warn",
      given: "$.paths[*][*]",
      then: {
        field: "description",
        function: "truthy"
      }
    },
    "no-unused-components": {
      severity: "warn"
    }
  }
};
