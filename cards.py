

class Card:
    def __init__(self, name, casting_cost, cmc, card_type, oracle_text, colors, card_subtypes=None, power=None, toughness=None, mana_produced=None, tags=None):
        self.name = name
        self.casting_cost = casting_cost
        self.cmc = cmc
        self.card_type = card_type
        self.oracle_text = oracle_text
        self.colors = colors
        self.card_subtypes = card_subtypes
        self.power = power
        self.toughness = toughness
        self.mana_produced = mana_produced
        self.tags = tags

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if self.name == other:
            return True
        else:
            return False

    def __hash__(self):
        return self.name


mana_providers = {
    "Simian Spirit Guide": Card("Simian Spirit Guide", "{2}{R}", 0, "creature", "Exile Simian Spirit Guide from your hand: Add {R}.", "R", mana_produced=1, tags=["single_use"]),
    "Mana Crypt": Card("Mana Crypt", "{0}", 0, "artifact", "At the beginning of your upkeep, flip a coin. If you lose the flip, Mana Crypt deals 3 damage to you. {T}: Add {C}{C}.", "C", mana_produced=2),
    "Mox Amber": Card("Mox Amber", "{0}", 0, "artifact", "{T}: Add one mana of any color among legendary creatures and planeswalkers you control.", "C", mana_produced=1),
    "Lotus Petal": Card("Lotus Petal", "{0}", 0, "artifact", "{T}, Sacrifice Lotus Petal: Add one mana of any color.", "C", mana_produced=1, tags=["single_use"]),
    "Chrome Mox": Card("Chrome Mox", "{0}", 0, "artifact", "Imprint — When Chrome Mox enters the battlefield, you may exile a nonartifact, nonland card from your hand. {T}: Add one mana of any of the exiled card’s colors.", "C", mana_produced=1),
    "Mox Diamond": Card("Mox Diamond", "{0}", 0, "artifact", "If Mox Diamond would enter the battlefield, you may discard a land card instead. If you do, put Mox Diamond onto the battlefield. If you don’t, put it into its owner’s graveyard. {T}: Add one mana of any color.", "C", mana_produced=1),
    "Mox Opal": Card("Mox Opal", "{0}", 0, "artifact", "Metalcraft — {T}: Add one mana of any color. Activate only if you control three or more artifacts.", "C", mana_produced=1),
    "Dark Ritual": Card("Dark Ritual", "{B}", 1, "instant", "Add {B}{B}{B}.", "B", mana_produced=3, tags=["single_use"]),
    "Rite of Flame": Card("Rite of Flame", "{R}", 1, "sorcery", "Add {R}{R}, then add {R} for each card named Rite of Flame in each graveyard.", "R", mana_produced=2, tags=["single_use"]),
    "Strike It Rich": Card("Strike It Rich", "{R}", 1, "sorcery", "Create a Treasure token. (It’s an artifact with “{T}, Sacrifice this artifact: Add one mana of any color.”) Flashback {2}{R} (You may cast this card from your graveyard for its flashback cost. Then exile it.)", "R", mana_produced=1, tags=["single_use"]),
    "Paradise Mantle": Card("Paradise Mantle", "{0}", 0, "artifact", "Equipped creature has “{T}: Add one mana of any color.” Equip {1}", "C", card_subtypes="equipment", mana_produced=1),
    "Springleaf Drum": Card("Springleaf Drum", "{1}", 1, "artifact", ", Tap an untapped creature you control: Add one mana of any color.", "C", mana_produced=1),
    "Culling the Weak": Card("Culling the Weak", "{B}", 1, "sorcery", "As an additional cost to cast this spell, sacrifice a creature. Add {B}{B}{B}{B}.", "B", mana_produced=4, tags=["single_use"]),
    "Infernal Plunge": Card("Infernal Plunge", "{R}", 1, "sorcery", "As an additional cost to cast this spell, sacrifice a creature. Add {R}{R}{R}.", "R", mana_produced=3, tags=["single_use"]),
    "Ragavan, Nimble Pilferer": Card("Ragavan, Nimble Pilferer", "{R}", 1, "creature", "Whenever Ragavan, Nimble Pilferer deals combat damage to a player, create a Treasure token and exile the top card of that player’s library. Until end of turn, you may cast that card. Dash {1}{R} (You may cast this spell for its dash cost. If you do, it gains haste, and it’s returned from the battlefield to its owner’s hand at the beginning of the next end step.)", "R", card_subtypes="monkey pirate", power=2, toughness=1, mana_produced=1),
    "Sol Ring": Card("Sol Ring", "{1}", 1, "artifact", "{T}: Add {C}{C}.", "C", mana_produced=2),
    "Mana Vault": Card("Mana Vault", "{1}", 1, "artifact", "Mana Vault doesn’t untap during your untap step. At the beginning of your upkeep, you may pay {4}. If you do, untap Mana Vault. At the beginning of your draw step, if Mana Vault is tapped, it deals 1 damage to you. {T}: Add {C}{C}{C}.", "C", mana_produced=3),
    "Cabal Ritual": Card("Cabal Ritual", "{1}{B}", 2, "instant", "Add {B}{B}{B}. Threshold — Add {B}{B}{B}{B}{B} instead if seven or more cards are in your graveyard.", "B", mana_produced=3, tags=["single_use"]),
    "Grim Monolith": Card("Grim Monolith", "{2}", 2, "artifact", "Grim Monolith doesn’t untap during your untap step. {T}: Add {C}{C}{C}. {4}: Untap Grim Monolith.", "C", mana_produced=3),
    "Dockside Extortionist": Card("Dockside Extortionist", "{1}{R}", 2, "creature", "When Dockside Extortionist enters the battlefield, create X Treasure tokens, where X is the number of artifacts and enchantments your opponents control.", "R", mana_produced=4, card_subtypes="goblin pirate", power=1, toughness=2, tags=["single_use"]),
    "Jeskas Will": Card("Jeskas Will", "{2}{R}", 3, "sorcery", "Choose one. If you control a commander as you cast this spell, you may choose both. • Add {R} for each card in target opponent’s hand. • Exile the top three cards of your library. You may play them this turn.", "R", mana_produced=5, tags=["single_use"]),
    "Arcane Signet": Card("Arcane Signet", "{2}", 2, "artifact", "{T}: Add one mana of any color in your commander’s color identity.", "C", mana_produced=1),
}



mana_artifacts = [
    "mana crypt",
    "sol ring",
    "mana vault",
    "grim monolith",
    "chrome mox",
    "mox diamond",
    "mox amber",
    "mox opal",
    "lotus petal",
    "arcane signet",
    "paradise mantle",
    "springleaf drum",
]
