let
  pkgs = let
    src = {
      url = https://github.com/NixOS/nixpkgs/archive/18bad38d3d928b7dd9ee09a38249dbeb217d34d1.tar.gz;
      sha256 = "1ajcyj9h83gski7y6wscwxj94ahlqf0j5r54yqs7wsjnc2adx5vc";
    };
  in import (fetchTarball src) {};

  inherit (pkgs) callPackage;
  latex = pkgs.texlive.combined.scheme-full;

in rec {

  # PDF version of the thesis
  thesis = callPackage ./nix/thesis {
    inherit latex thesis-source python;
  };

  # PDF version of thesis announcement
  thesis-announcement = callPackage ./nix/announcement {
    inherit latex thesis-source;
  };

  # Standalone source tree containing everything needed to build the thesis.
  thesis-source = callPackage ./nix/thesis-source {
    inherit references media;
  };



#   references = ./data/library.bib; #/home/freddy/Data/Media/References/library.bib;
  references = /home/freddy/Data/Media/References/library.bib;

  # Media: figures and audio
  media = {
    # Step-by-step add propagation effects
    propagation = callPackage ./nix/media/propagation {
      inherit python;
      inherit (lib) matplotlibHook;
    };
    # Basic sound, attenuation
    sound = callPackage ./nix/media/sound {
      inherit python;
      inherit (lib) matplotlibHook;
    };
    # Signal processing. Convolution.
    signal-processing = callPackage ./nix/media/signal-processing {
      inherit python;
      inherit (lib) matplotlibHook;
    };
    # Distant source with aircraft-like spectrum. Atmospheric turbulence.
    propagation-distant = callPackage ./nix/media/propagation-distant {
      inherit python;
      inherit (lib) matplotlibHook to_wav;
    };
    # From recording to auralisation. Samples from second paper.
    recording-to-auralisation = callPackage ./nix/media/recording-to-auralisation {
      inherit python;
      inherit (lib) matplotlibHook to_wav;
    };
  };

  lib = callPackage ./nix/lib {
    inherit python;
  };

  # Python interpreter that has extra packages available
  python = callPackage ./nix/packages { };

  # Papers that are appended to the thesis
  papers = {
    overview = ./data/papers/overview.pdf;
    turbulence = ./data/papers/turbulence.pdf;
  };
}
