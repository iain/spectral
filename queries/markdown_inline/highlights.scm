;; extends

; Narrower captures so a link's address and reference label can be dimmed
; while autolinks, which share @markup.link.url, stay styled as links. Any
; colorscheme that does not define them falls back to the parent capture.

(inline_link
  (link_destination) @markup.link.url.destination)

(image
  (link_destination) @markup.link.url.destination)

(full_reference_link
  (link_label) @markup.link.label.reference)
