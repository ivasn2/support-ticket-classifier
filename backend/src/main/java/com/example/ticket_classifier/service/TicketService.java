package com.example.ticket_classifier.service;

import com.example.ticket_classifier.dto.CreateTicketRequest;
import com.example.ticket_classifier.entity.Ticket;
import com.example.ticket_classifier.entity.TicketStatus;
import com.example.ticket_classifier.repository.TicketRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.time.LocalDateTime;
import java.util.List;

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

    public List<Ticket> getAll() {
        return ticketRepository.findAll();
    }

    public Ticket getById(Long id) {
        return ticketRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Ticket not found"));
    }

    public Ticket updateStatus(Long id, TicketStatus status) {
        Ticket ticket = getById(id);
        ticket.setStatus(status);
        if (status == TicketStatus.RESOLVED) {
            ticket.setAnsweredAt(LocalDateTime.now());
        }
        return ticketRepository.save(ticket);
    }
}
