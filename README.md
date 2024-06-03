# 🛍️ ProShop

Welcome to **ProShop** - Your one-stop shop for all your shopping needs! 🛒

## 🩹 Resolving Errors 🩹

### ⚠️ Common Error: `ERR_OSSL_EVP_UNSUPPORTED`

If you encounter an error similar to the following:

opensslErrorStack: [ 'error:03000086
envelope routines::initialization error' ],
library: 'digital envelope routines',
reason: 'unsupported',
code: 'ERR_OSSL_EVP_UNSUPPORTED'

**Node.js Version**: v18.17.1

#### 🛠️ Solution:

Include the following in your `package.json` file:

```json
"scripts": {
  "start": "react-scripts --openssl-legacy-provider start",
  "build": "react-scripts --openssl-legacy-provider build",
  "test": "react-scripts --openssl-legacy-provider test"
}
```

### ⚠️ Common Error: React must be in scope when using JSX"``

#### 🛠️ Solution:
Import React at the top of your App.js file (or the file which is producing the error):

import React from 'react';


