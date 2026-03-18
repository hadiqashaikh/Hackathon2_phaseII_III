self.__BUILD_MANIFEST = {
  "__rewrites": {
    "afterFiles": [
      {
        "source": "/api/chat/:path*"
      },
      {
        "source": "/api/tasks/:path*"
      },
      {
        "source": "/api/quick-tasks/:path*"
      },
      {
        "source": "/api/auth/me"
      }
    ],
    "beforeFiles": [],
    "fallback": []
  },
  "sortedPages": [
    "/_app",
    "/_error"
  ]
};self.__BUILD_MANIFEST_CB && self.__BUILD_MANIFEST_CB()