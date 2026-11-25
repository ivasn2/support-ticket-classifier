package com.example.ticket_classifier.dto;

import com.example.ticket_classifier.entity.TicketStatus;

public class UpdateTicketStatusRequest {
    private TicketStatus status;

    public TicketStatus getStatus() {
        return status;
    }

    public void setStatus(TicketStatus status) {
        this.status = status;
    }
}