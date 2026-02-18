return {
  {
    "folke/tokyonight.nvim",
    priority = 1000,
    init = function()
      vim.o.background = "dark"
    end,
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "tokyonight-night",
    },
  },
}
