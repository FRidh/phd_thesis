# PhD thesis

This repository contains the code and data that I used to write my PhD thesis.
The thesis can be build reproducibly using Nix

```nix
nix-build -A thesis
```

Note that Nix 1.12 or higher needs to be used because `fetchTarball` with a `sha256` hash is extensively used.
