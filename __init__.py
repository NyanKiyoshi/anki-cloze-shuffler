from aqt import gui_hooks
from anki.cards import Card

JS_SHUFFLER = r"""

// Shuffles child nodes of a given HTML node (in-place)
function shuffleNode(node) {
    const frag = document.createDocumentFragment();
    const arr = [...node.childNodes];

    // Shuffle the array in-place (uses Sattolo's algorithm)
    let i = arr.length - 1;
    while (i > 0) {
        const j = Math.floor(Math.random() * i);
        if (j !== i) {
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        --i;
    }
    arr.forEach((el) => frag.appendChild(el));

    // Apply changes
    node.replaceChildren(frag);
}

// Shuffles all 'li' and 'ol' lists that contain cloze(s).
function shuffleAllLists(onlyShuffleClozes) {

    // Note: we use `class*=cloze` selector in order to support add-ons
    //       (such as 'Enhanced Cloze').
    //       When not using any add-ons, `:has(.cloze)` selector is enough.
    const selector = onlyShuffleClozes
        ? 'ul:has([class*="cloze"]), ol:has([class*="cloze"])'
        : 'ul, ol';

    document.querySelectorAll(selector).forEach((el) => shuffleNode(el));
}
"""


def on_card_will_show(text: str, card: Card, kind: str) -> str:
    """
    Injects cloze javascript shuffler inside the card's HTML before rendering.
    """
    note = card.note()
    shuffle = False

    if (shuffle_clozes := note.has_tag("shuffle-clozes")) or note.has_tag("shuffle"):

        # Store as javascript syntax, will be passed to the JS script
        shuffle_only_clozes = "true" if shuffle_clozes else "false"

        text = text + (
            f"<script>{JS_SHUFFLER}\n"
            f"shuffleAllLists({shuffle_only_clozes})</script>"
        )
    return text


gui_hooks.card_will_show.append(on_card_will_show)
