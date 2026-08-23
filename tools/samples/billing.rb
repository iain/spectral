# frozen_string_literal: true

require "money"

module Billing
  # Adds VAT to a set of line items and renders an invoice total.
  class InvoiceCalculator
    extend T::Sig

    VAT_RATE = 0.21
    CURRENCIES = %i[eur gbp usd].freeze

    sig { params(items: T::Array[LineItem]).returns(Money) }
    def self.total_for(items)
      items.sum(Money.zero) { |item| item.amount * (1 + VAT_RATE) }
    end

    def initialize(customer:, currency: :eur)
      raise ArgumentError, "unknown currency #{currency}" unless CURRENCIES.include?(currency)

      @customer = customer
      @currency = currency
      @lines    = []
    end

    sig { params(description: String, cents: Integer).returns(T.self_type) }
    def add(description, cents)
      return self if cents.zero?

      @lines << { description: description, cents: cents, added_at: Time.now }
      self
    end

    def to_s
      format("%<name>s owes %<total>.2f %<cur>s",
             name: @customer.name, total: total / 100.0, cur: @currency.to_s.upcase)
    end
  end
end
