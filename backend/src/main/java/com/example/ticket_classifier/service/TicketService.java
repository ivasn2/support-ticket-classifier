package com.example.ticket_classifier.service;

import com.example.ticket_classifier.dto.CreateTicketRequest;
import com.example.ticket_classifier.entity.Ticket;
import com.example.ticket_classifier.repository.TicketRepository;
import org.springframework.stereotype.Service;

@Service
public class TicketService {

    private final TicketRepository ticketRepository;

    public TicketService(TicketRepository ticketRepository) {

        this.ticketRepository = ticketRepository;
    }

    public Ticket create(CreateTicketRequest request) {
        Ticket ticket = new Ticket();
        ticket.setTitle(request.getTitle());
        ticket.setDescription(request.getDescription());
        return ticketRepository.save(ticket);
    }

}
