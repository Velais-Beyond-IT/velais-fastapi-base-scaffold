# CORS Configuration Guide

## 🔒 Security-First CORS Configuration

This project implements environment-aware CORS configuration that balances development convenience with production security.

## 📋 Configuration Overview

### Environment Variables

| Variable | Description | Development | Staging | Production |
|----------|-------------|-------------|---------|------------|
| `CORS_ORIGINS` | Allowed origins | `*` | `https://staging.app.com` | `https://app.com,https://www.app.com` |
| `CORS_ALLOW_CREDENTIALS` | Allow cookies/auth | `true` | `true` | `true` |
| `CORS_ALLOW_METHODS` | HTTP methods | `*` | `GET,POST,PUT,DELETE,OPTIONS,PATCH` | `GET,POST,PUT,DELETE,OPTIONS,PATCH` |
| `CORS_ALLOW_HEADERS` | Request headers | `*` | `Authorization,Content-Type,Accept` | `Authorization,Content-Type,Accept` |
| `CORS_MAX_AGE` | Preflight cache | `86400` | `86400` | `86400` |

## 🛡️ Security Features

### Automatic Environment Detection
- **Development**: Allows `*` origins for fast development
- **Production/Staging**: Requires specific HTTPS origins only
- **Validation**: Invalid origins are rejected at startup

### Built-in Security Checks
```python
from src.utils.cors import is_cors_secure

# Automatically validates CORS configuration
assert is_cors_secure(["*"], "development") is True        # ✅ OK in dev
assert is_cors_secure(["*"], "production") is False        # ❌ Not secure in prod
assert is_cors_secure(["https://app.com"], "production") is True  # ✅ Secure
```

## 📝 Configuration Examples

### Development Environment
```env
ENV=development
CORS_ORIGINS=*
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*
```

**Result**: Maximum convenience, all origins allowed.

### Staging Environment
```env
ENV=staging
CORS_ORIGINS=https://staging.yourapp.com,https://staging-admin.yourapp.com
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,OPTIONS,PATCH
CORS_ALLOW_HEADERS=Authorization,Content-Type,X-Requested-With,Accept,Origin
```

**Result**: Secure configuration for staging testing.

### Production Environment
```env
ENV=production
CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com,https://admin.yourapp.com
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,OPTIONS,PATCH
CORS_ALLOW_HEADERS=Authorization,Content-Type,X-Requested-With,Accept,Origin
```

**Result**: Maximum security, only trusted domains.

## 🔧 Usage in Code

### Settings Access
```python
from src.config.settings import settings

# Get environment-appropriate origins
origins = settings.get_cors_origins()

# In development: ["*"]
# In production: ["https://yourapp.com", "https://admin.yourapp.com"]
```

### Manual Validation
```python
from src.utils.cors import validate_origin, is_cors_secure

# Validate individual origins
assert validate_origin("https://example.com") is True
assert validate_origin("invalid-url") is False

# Check security for environment
origins = ["https://secure.com"]
assert is_cors_secure(origins, "production") is True
```

## 🚨 Security Best Practices

### ✅ DO:
- **Use HTTPS in production**: Never allow `http://` origins in production (except localhost)
- **Specify exact domains**: List only the domains you control
- **Test configurations**: Use the provided test utilities
- **Environment separation**: Different settings per environment
- **Validate at startup**: Invalid configurations fail fast

### ❌ DON'T:
- **Wildcard in production**: Never use `*` in staging/production
- **HTTP in production**: Avoid `http://` origins in production
- **Too permissive headers**: Don't use `*` for headers in production
- **Ignore validation errors**: Always fix CORS validation issues

## 🔬 Testing CORS Configuration

### Unit Tests
```bash
# Run CORS-specific tests
uv run pytest tests/test_cors.py -v

# Test specific functionality
uv run pytest tests/test_cors.py::test_cors_configuration_integration -v
```

### Manual Testing
```bash
# Test different environments
ENV=development uv run python -c "from src.config.settings import settings; print(settings.get_cors_origins())"
ENV=production CORS_ORIGINS=https://example.com uv run python -c "from src.config.settings import settings; print(settings.get_cors_origins())"
```

### Browser Testing
```javascript
// Test CORS from browser console
fetch('http://localhost:8000/api/v1/health', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
}).then(response => response.json()).then(data => console.log(data));
```

## 🐳 Docker Configuration

### Development
```dockerfile
ENV ENV=development
# CORS_ORIGINS will default to "*"
```

### Staging
```dockerfile
ENV ENV=staging
ENV CORS_ORIGINS=https://staging.yourapp.com
```

### Production
```dockerfile
ENV ENV=production
ENV CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com
```

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] **Set `ENV=production`**
- [ ] **Configure specific `CORS_ORIGINS`** (no wildcards)
- [ ] **Use HTTPS origins only**
- [ ] **Specify exact methods and headers**
- [ ] **Test CORS configuration**
- [ ] **Verify no wildcard usage**
- [ ] **Run security validation tests**

## 🆘 Troubleshooting

### Common Issues

**CORS Error in Browser**:
```
Access to fetch at 'https://api.yourapp.com' from origin 'https://yourapp.com'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header
```

**Solution**: Add your frontend domain to `CORS_ORIGINS`:
```env
CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com
```

**Invalid Origin Error**:
```
ValueError: Invalid origin format: invalid-url. Must start with http:// or https://
```

**Solution**: Fix the origin format:
```env
# ❌ Wrong
CORS_ORIGINS=myapp.com

# ✅ Correct
CORS_ORIGINS=https://myapp.com
```

**Wildcard Not Working in Production**:
```python
# In production, wildcard origins return empty list for security
settings.get_cors_origins()  # Returns [] instead of ["*"]
```

**Solution**: Specify exact origins for production:
```env
CORS_ORIGINS=https://yourapp.com,https://admin.yourapp.com
```

## 📚 Additional Resources

- **FastAPI CORS Documentation**: https://fastapi.tiangolo.com/tutorial/cors/
- **MDN CORS Guide**: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- **OWASP CORS Security**: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Origin_Resource_Sharing_Cheat_Sheet.html

This configuration ensures your API is both developer-friendly and production-secure! 🚀
